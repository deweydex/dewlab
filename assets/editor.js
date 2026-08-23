/* The editor: reorder a series, insert a tutorial, create one, and edit what
 * is inside it — against the repository, through the GitHub API, committed to
 * a branch and opened as a pull request.
 *
 * It edits *source*, not the built site. Everything here reads and writes the
 * markdown in tutorials/ and the order file beside it, because that is what a
 * person actually changes; site/ is a derived artefact and editing it would be
 * editing the output of a build.
 *
 * Never linked from a student page. It is for Josh and whoever edits with him.
 */

const API = "https://api.github.com";
const TOKEN_KEY = "dewlab:editor:token";
const REPO = "deweydex/dewlab";

/* ------------------------------------------------------------------ parsing
 *
 * The build decides what a cell is by finding ```python exec fences and
 * reading the `id:` line inside. The editor has to agree with it exactly,
 * because a disagreement here is an editor that shows you something the build
 * will not produce. Kept as pure functions so the tests can drive them without
 * a network or a token.
 */

const FENCE = /^ *```([^\n]*)\n([\s\S]*?)^ *```[ \t]*$/gm;

export function splitFrontmatter(text) {
  if (!text.startsWith("---")) return { meta: "", body: text };
  const end = text.indexOf("\n---", 3);
  if (end === -1) return { meta: "", body: text };
  return { meta: text.slice(3, end).trim(), body: text.slice(end + 4).replace(/^\n+/, "") };
}

export function frontmatterField(meta, field) {
  const line = meta.split("\n").find((l) => l.startsWith(field + ":"));
  if (!line) return "";
  return line.slice(field.length + 1).trim().replace(/^"(.*)"$/, "$1");
}

export const STATUSES = ["draft", "beta", "live", "archived"];

export function setFrontmatterField(meta, field, value) {
  /* Set a field, or add it if it is not there. Added after `version:` rather
   * than at the end, because the end of the frontmatter is where `covers:`
   * lives and its indented children would swallow anything put below them. */
  const lines = meta.split("\n");
  const at = lines.findIndex((l) => l.startsWith(field + ":"));
  if (at !== -1) {
    lines[at] = `${field}: ${value}`;
    return lines.join("\n");
  }
  const after = lines.findIndex((l) => l.startsWith("version:"));
  const where = after === -1 ? lines.length - 1 : after;
  lines.splice(where + 1, 0, `${field}: ${value}`);
  return lines.join("\n");
}

export function statusOf(text) {
  return frontmatterField(splitFrontmatter(text).meta, "status") || "live";
}

export function parseCells(body) {
  /* Every exec-tagged fence, with the id the build will key saved work on.
   * An untagged fence is illustrative code and is not a cell, which is the
   * same rule build.py applies. */
  const cells = [];
  FENCE.lastIndex = 0;
  let match;
  while ((match = FENCE.exec(body)) !== null) {
    const info = match[1].trim();
    if (!/^python\s+exec\b/.test(info)) continue;
    const lines = match[2].split("\n");
    let id = "";
    let hint = "";
    let start = 0;
    for (; start < lines.length; start += 1) {
      const header = /^\s*(id|hint)\s*:\s*(.*)$/.exec(lines[start]);
      if (!header) break;
      if (header[1] === "id") id = header[2].trim();
      else hint = header[2].trim();
    }
    cells.push({
      id,
      hint,
      code: lines.slice(start).join("\n").replace(/\n+$/, ""),
      at: match.index,
      length: match[0].length,
    });
  }
  return cells;
}

export function headings(body) {
  return [...body.matchAll(/^(#{1,3})\s+(.+?)\s*$/gm)].map((m) => ({
    level: m[1].length,
    text: m[2],
  }));
}

export function problems(body) {
  /* What the build would refuse, found before the commit rather than after.
   * This is the whole justification for not shipping a visual preview: the
   * mistakes that actually happen are structural, and structure is the part a
   * browser can check honestly. */
  const found = [];
  const cells = parseCells(body);
  const seen = new Map();
  for (const cell of cells) {
    if (!cell.id) {
      found.push({ level: "error", text: "A runnable cell has no id: line. The build stops on this." });
      continue;
    }
    if (!/^[a-z0-9-]+$/.test(cell.id)) {
      found.push({ level: "error", text: `Cell id "${cell.id}" is not lowercase letters, digits and hyphens.` });
    }
    seen.set(cell.id, (seen.get(cell.id) || 0) + 1);
  }
  for (const [id, count] of seen) {
    if (count > 1) {
      found.push({ level: "error", text: `Cell id "${id}" is used ${count} times. Ids must be unique in a page.` });
    }
  }
  const fences = (body.match(/^ *```/gm) || []).length;
  if (fences % 2 !== 0) {
    found.push({ level: "error", text: "A code fence is opened and never closed." });
  }
  if (!headings(body).some((h) => h.level === 1)) {
    found.push({ level: "warn", text: "No level-one heading. The page will have no title on it." });
  }
  return found;
}

export function renamedCells(before, after) {
  /* A cell's id is the key a student's saved work is stored under. Renaming
   * one does not move their work: it orphans it, and the cell comes back
   * empty. Nothing in the build can warn about this, because by then the
   * rename has happened — so the editor has to, while both versions exist. */
  const was = parseCells(before);
  const now = parseCells(after);
  const gone = [];
  const nowIds = new Set(now.map((c) => c.id));
  for (const cell of was) {
    if (cell.id && !nowIds.has(cell.id)) gone.push(cell.id);
  }
  return gone;
}

/* --------------------------------------------------------------- the client
 *
 * Swappable so the browser tests can drive the whole editor without a token
 * or a network. `start()` takes one, and the page passes the real one.
 */

export function githubClient(token) {
  async function call(path, options = {}) {
    const response = await fetch(API + path, {
      ...options,
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...(options.headers || {}),
      },
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(`GitHub said ${response.status}: ${detail.slice(0, 300)}`);
    }
    return response.status === 204 ? null : response.json();
  }

  return {
    async listTutorials() {
      const head = await call(`/repos/${REPO}/git/ref/heads/main`);
      const tree = await call(`/repos/${REPO}/git/trees/${head.object.sha}?recursive=1`);
      return {
        base: head.object.sha,
        paths: tree.tree
          .filter((e) => e.type === "blob" && e.path.startsWith("tutorials/"))
          .map((e) => e.path),
      };
    },
    async read(path) {
      const file = await call(`/repos/${REPO}/contents/${encodeURI(path)}?ref=main`);
      return decodeURIComponent(escape(atob(file.content.replace(/\n/g, ""))));
    },
    async commit({ base, branch, message, files }) {
      /* One commit for the whole change, through the git data API, rather than
       * one commit per file through the contents API. An insertion touches a
       * markdown file and an order file, and those two arriving separately
       * would leave main briefly describing a series that does not exist. */
      const blobs = [];
      for (const file of files) {
        const blob = await call(`/repos/${REPO}/git/blobs`, {
          method: "POST",
          body: JSON.stringify({ content: file.text, encoding: "utf-8" }),
        });
        blobs.push({ path: file.path, mode: "100644", type: "blob", sha: blob.sha });
      }
      const tree = await call(`/repos/${REPO}/git/trees`, {
        method: "POST",
        body: JSON.stringify({ base_tree: base, tree: blobs }),
      });
      const created = await call(`/repos/${REPO}/git/commits`, {
        method: "POST",
        body: JSON.stringify({ message, tree: tree.sha, parents: [base] }),
      });
      await call(`/repos/${REPO}/git/refs`, {
        method: "POST",
        body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: created.sha }),
      });
      const pull = await call(`/repos/${REPO}/pulls`, {
        method: "POST",
        body: JSON.stringify({
          title: message.split("\n")[0],
          head: branch,
          base: "main",
          draft: true,
          body: `Written from the dewlab editor.\n\n${message}`,
        }),
      });
      return pull.html_url;
    },
  };
}

/* ------------------------------------------------------------------ the page */

/* What each one does, in the tooltip, because four words on four buttons is
 * not enough to tell draft from beta and the difference matters. */
const STATUS_MEANS = {
  draft: "Not published at all. No page is built, so nobody can reach it.",
  beta: "Published but not on the course. Anyone with the link can read it; "
      + "students are not sent to it.",
  live: "On the course, in the reading order.",
  archived: "Was on the course, is not now. Stays readable, keeps saved work.",
};

const TEMPLATE = `---
title: "{title}"
slug: {slug}
module: {module}
module_title: "{module_title}"
year: "{year}"
series: {series}
version: 1
---

# {title}

Write the opening here — what this tutorial is for, and why it comes after the
one before it.

## A first section

\`\`\`python exec
id: a-first-section-1
# The first thing a student runs.
\`\`\`

## Reflection

What surprised you here, and what would you like to understand better?
`;

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (value !== null && value !== undefined) node.setAttribute(key, value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

function slugify(title) {
  return title.toLowerCase().replace(/[^\w\s-]/g, "").trim().replace(/[\s_]+/g, "-");
}

export function start(root, client, { onStatus = () => {} } = {}) {
  const state = { series: new Map(), files: new Map(), base: null, editing: null, dirty: new Set() };

  function status(text, kind = "note") {
    onStatus(text, kind);
    const bar = document.getElementById("dl-editor-status");
    if (bar) {
      bar.textContent = text;
      bar.dataset.kind = kind;
      bar.hidden = !text;
    }
  }

  async function load() {
    status("Reading the repository…");
    const { base, paths } = await client.listTutorials();
    state.base = base;
    state.files.clear();
    state.series.clear();
    for (const path of paths) {
      const text = await client.read(path);
      state.files.set(path, text);
    }
    for (const [path, text] of state.files) {
      if (!path.endsWith(".order.yaml")) continue;
      const module = path.split("/")[1];
      const name = path.split("/").pop().replace(".order.yaml", "");
      const order = [...text.matchAll(/^ *- +(\S+)\s*$/gm)].map((m) => m[1]);
      const titled = /^series:\s*(.+)$/m.exec(text);
      state.series.set(path, {
        path, module, name, order,
        title: titled ? titled[1].trim() : name,
        /* Everything belonging to this series, whether or not it is on the
         * route. Without this, setting a tutorial to draft would drop it out
         * of the order file and out of the list at once — a one-way trip, with
         * no way back to it in the editor. */
        off: [],
      });
    }

    for (const [path, text] of state.files) {
      if (path.endsWith(".order.yaml") || !path.endsWith(".md")) continue;
      const meta = splitFrontmatter(text).meta;
      const module = frontmatterField(meta, "module");
      const slug = frontmatterField(meta, "slug");
      const series = [...state.series.values()].find(
        (s) => s.module === module && !s.order.includes(slug)
          && frontmatterField(meta, "series") === s.name
      );
      if (series) series.off.push(slug);
    }
    status("");
    render();
  }

  function pathOf(module, slug) {
    return `tutorials/${module}/${slug}.md`;
  }

  function titleOf(module, slug) {
    const text = state.files.get(pathOf(module, slug));
    if (!text) return slug;
    return frontmatterField(splitFrontmatter(text).meta, "title") || slug;
  }

  /* ------------------------------------------------------------ the list view */

  function move(series, from, to) {
    if (to < 0 || to >= series.order.length || from === to) return;
    const moved = series.order.splice(from, 1)[0];
    series.order.splice(to, 0, moved);
    state.dirty.add(series.path);
    render();
  }

  function insert(series, at) {
    const title = prompt("What is the new tutorial called?");
    if (!title) return;
    const slug = slugify(title);
    if (series.order.includes(slug)) {
      status(`This series already has a ${slug}.`, "error");
      return;
    }
    const sibling = state.files.get(pathOf(series.module, series.order[0])) || "";
    const meta = splitFrontmatter(sibling).meta;
    const body = TEMPLATE
      .replaceAll("{title}", title)
      .replaceAll("{slug}", slug)
      .replaceAll("{module}", series.module)
      .replaceAll("{module_title}", frontmatterField(meta, "module_title") || series.module)
      .replaceAll("{year}", frontmatterField(meta, "year") || "2026-2027")
      .replaceAll("{series}", frontmatterField(meta, "series") || series.name);
    state.files.set(pathOf(series.module, slug), body);
    series.order.splice(at, 0, slug);
    state.dirty.add(series.path);
    state.dirty.add(pathOf(series.module, slug));
    render();
  }

  function setStatus(series, slug, status) {
    /* One gesture, two files. A status change is not just a frontmatter edit:
     * only a live tutorial is on the reading order, and the build refuses an
     * order file that lists anything else — so the line has to move with the
     * field or the next build stops. Doing that by hand is the part worth
     * automating; the field on its own is trivial. */
    const path = pathOf(series.module, slug);
    const text = state.files.get(path);
    if (!text) return;
    const { meta, body } = splitFrontmatter(text);
    state.files.set(path, `---\n${setFrontmatterField(meta, "status", status)}\n---\n\n${body}`);
    state.dirty.add(path);

    const at = series.order.indexOf(slug);
    const off = series.off.indexOf(slug);
    if (status === "live" && at === -1) {
      series.order.push(slug);
      if (off !== -1) series.off.splice(off, 1);
      state.dirty.add(series.path);
    } else if (status !== "live" && at !== -1) {
      series.order.splice(at, 1);
      if (off === -1) series.off.push(slug);
      state.dirty.add(series.path);
    }
    render();
  }

  function statusControl(series, slug) {
    const now = statusOf(state.files.get(pathOf(series.module, slug)) || "");
    return el("span", { class: "dl-editor-status", "data-status": now },
      ...STATUSES.map((status) => el("button", {
        type: "button",
        class: "dl-editor-status-option",
        "data-status": status,
        "aria-pressed": String(status === now),
        title: STATUS_MEANS[status],
        onclick: () => setStatus(series, slug, status),
      }, status)));
  }

  function seriesView(series) {
    const list = el("ol", { class: "dl-editor-list", "data-series": series.name });
    series.order.forEach((slug, index) => {
      const card = el("li", {
        class: "dl-editor-card", draggable: "true", "data-slug": slug, "data-index": index,
        ondragstart: (ev) => { ev.dataTransfer.setData("text/plain", String(index)); },
        ondragover: (ev) => ev.preventDefault(),
        ondrop: (ev) => {
          ev.preventDefault();
          move(series, Number(ev.dataTransfer.getData("text/plain")), index);
        },
      },
        el("span", { class: "dl-editor-pos" }, index + 1),
        el("button", {
          class: "dl-editor-open", type: "button",
          onclick: () => { state.editing = { series, slug }; render(); },
        }, titleOf(series.module, slug)),
        statusControl(series, slug),
        el("span", { class: "dl-editor-moves" },
          el("button", { type: "button", class: "dl-editor-up", "aria-label": `Move ${slug} earlier`,
                         onclick: () => move(series, index, index - 1) }, "↑"),
          el("button", { type: "button", class: "dl-editor-down", "aria-label": `Move ${slug} later`,
                         onclick: () => move(series, index, index + 1) }, "↓"),
        ),
      );
      list.append(
        el("li", { class: "dl-editor-gap" },
          el("button", { type: "button", onclick: () => insert(series, index) }, "insert here")),
        card,
      );
    });
    list.append(
      el("li", { class: "dl-editor-gap" },
        el("button", { type: "button", class: "dl-editor-new",
                       onclick: () => insert(series, series.order.length) }, "new tutorial at the end")),
    );
    /* Off the route but still here: drafts, betas, and anything archived. They
     * have no position, so they carry no number and no move arrows — only what
     * they are, and the way back to live. */
    for (const slug of series.off) {
      list.append(el("li", { class: "dl-editor-card dl-editor-off", "data-slug": slug },
        el("span", { class: "dl-editor-pos" }, "—"),
        el("button", {
          class: "dl-editor-open", type: "button",
          onclick: () => { state.editing = { series, slug }; render(); },
        }, titleOf(series.module, slug)),
        statusControl(series, slug),
      ));
    }
    return el("section", { class: "dl-editor-series" },
      el("h2", {}, series.title),
      el("p", { class: "dl-editor-where" }, series.path),
      list);
  }

  /* ------------------------------------------------------- the tutorial view */

  function editorView({ series, slug }) {
    const path = pathOf(series.module, slug);
    const original = state.files.get(path) || "";
    const { meta, body } = splitFrontmatter(original);

    const area = el("textarea", { class: "dl-editor-body", spellcheck: "true", rows: "28" });
    area.value = body;

    const report = el("div", { class: "dl-editor-report", id: "dl-editor-report" });

    function check() {
      const next = area.value;
      report.replaceChildren();
      const gone = renamedCells(body, next);
      if (gone.length) {
        report.append(el("p", { class: "dl-editor-danger" },
          `Renaming a cell id throws away the work every student saved in it. ` +
          `These ids are no longer here: ${gone.join(", ")}.`));
      }
      for (const problem of problems(next)) {
        report.append(el("p", { class: `dl-editor-${problem.level}` }, problem.text));
      }
      const cells = parseCells(next);
      report.append(el("p", { class: "dl-editor-structure" },
        `${cells.length} runnable cell${cells.length === 1 ? "" : "s"}, ` +
        `${headings(next).length} headings. ` +
        `This is what the build will see — it is not a picture of the page.`));
    }

    area.addEventListener("input", () => {
      state.files.set(path, `---\n${meta}\n---\n\n${area.value}`);
      state.dirty.add(path);
      check();
    });
    check();

    return el("section", { class: "dl-editor-one" },
      el("p", {},
        el("button", { type: "button", class: "dl-editor-back",
                       onclick: () => { state.editing = null; render(); } }, "← all tutorials")),
      el("h2", {}, frontmatterField(meta, "title") || slug),
      el("p", { class: "dl-editor-where" }, path),
      el("details", { class: "dl-editor-meta" },
        el("summary", {}, "Frontmatter"),
        el("pre", {}, meta)),
      area,
      report);
  }

  /* ------------------------------------------------------------- committing */

  function orderText(series) {
    const original = state.files.get(series.path) || "";
    const head = original.split(/^order:/m)[0];
    return `${head}order:\n${series.order.map((s) => `  - ${s}\n`).join("")}`;
  }

  async function save() {
    if (!state.dirty.size) {
      status("Nothing has changed.", "note");
      return;
    }
    const message = prompt("What did you change? (this becomes the commit message)");
    if (!message) return;
    const files = [];
    for (const path of state.dirty) {
      const series = state.series.get(path);
      files.push({ path, text: series ? orderText(series) : state.files.get(path) });
    }
    status(`Committing ${files.length} file${files.length === 1 ? "" : "s"}…`);
    try {
      const branch = `editor/${slugify(message).slice(0, 40)}-${Date.now().toString(36)}`;
      const url = await client.commit({ base: state.base, branch, message, files });
      state.dirty.clear();
      /* Render first: it rebuilds the status bar, so setting the message
       * before it would write into an element about to be thrown away. */
      render();
      status(`Opened ${url}`, "done");
    } catch (error) {
      status(String(error.message || error), "error");
    }
  }

  /* ------------------------------------------------------------------ render */

  function render() {
    root.replaceChildren();
    root.append(
      el("div", { class: "dl-editor-bar" },
        el("button", { type: "button", id: "dl-editor-save", onclick: save,
                       disabled: state.dirty.size ? null : "disabled" },
           state.dirty.size ? `Commit ${state.dirty.size} change${state.dirty.size === 1 ? "" : "s"}` : "Nothing to commit"),
        el("button", { type: "button", id: "dl-editor-forget", onclick: () => {
          try { localStorage.removeItem(TOKEN_KEY); } catch (e) { /* blocked storage */ }
          location.reload();
        } }, "Forget my token"),
      ),
      el("div", { class: "dl-editor-status", id: "dl-editor-status", role: "status", hidden: "hidden" }),
    );
    if (state.editing) root.append(editorView(state.editing));
    /* By the name shown, not the filename behind it. Sorting a visible list on
     * an invisible key puts things in an order nobody can predict. */
    else for (const series of [...state.series.values()].sort((a, b) => a.title.localeCompare(b.title))) {
      root.append(seriesView(series));
    }
  }

  globalThis.dewlabEditor = {
    state, load, save, render, move, insert, setStatus, setFrontmatterField,
  };
  return load();
}

/* The token gate. Kept separate from start() so the tests can drive the editor
 * without one, and so the trade is stated where somebody has to read it. */
export function gate(root) {
  let token = null;
  try { token = localStorage.getItem(TOKEN_KEY); } catch (e) { /* blocked storage */ }
  if (token) return start(root, githubClient(token));

  const field = el("input", { type: "password", id: "dl-editor-token",
                              placeholder: "github_pat_…", autocomplete: "off" });
  root.replaceChildren(el("form", {
    class: "dl-editor-gate",
    onsubmit: (ev) => {
      ev.preventDefault();
      if (!field.value.trim()) return;
      try { localStorage.setItem(TOKEN_KEY, field.value.trim()); } catch (e) { /* blocked storage */ }
      start(root, githubClient(field.value.trim()));
    },
  },
    el("p", {}, "This page edits the repository directly. It needs a GitHub " +
                "fine-grained token with contents and pull-request write on " +
                REPO + ", and nothing else."),
    el("p", { class: "dl-editor-warn" },
      "The token is kept in this browser's local storage. On your own machine " +
      "that is a fair trade; on a shared one it is not. There is a button to " +
      "forget it, and this page is never linked from anywhere students go."),
    field,
    el("button", { type: "submit" }, "Start editing"),
  ));
}

if (typeof document !== "undefined" && document.getElementById("dl-editor")) {
  gate(document.getElementById("dl-editor"));
}
